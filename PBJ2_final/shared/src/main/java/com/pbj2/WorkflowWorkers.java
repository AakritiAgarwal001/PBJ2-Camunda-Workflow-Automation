package com.pbj2;

import io.camunda.client.annotation.JobWorker;
import io.camunda.client.annotation.Variable;
import java.math.BigDecimal;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.stereotype.Component;

/**
 * External workers shared by the three PBJ-2 Camunda 8 workflows.
 * All test data is synthetic. The simulate* flags are only for controlled failure testing.
 */
@Component
public class WorkflowWorkers {

  private static final ObjectMapper JSON = new ObjectMapper();
  private static final HttpClient HTTP = HttpClient.newBuilder()
      .connectTimeout(Duration.ofSeconds(10)).build();

  @Value("${pbj2.mock-api.base-url:http://localhost:8081}")
  private String mockApiBaseUrl;

  @JobWorker(type = "validate-applicant", autoComplete = true)
  public Map<String, Object> validateApplicant(
      @Variable String applicantId,
      @Variable String applicantName,
      @Variable BigDecimal requestedLoanAmount,
      @Variable BigDecimal monthlyIncome,
      @Variable String employmentStatus,
      @Variable String creditHistory,
      @Variable Boolean simulateWorkerFailure) {
    failOnRequest(simulateWorkerFailure, "validate-applicant");
    String issue = null;
    if (blank(applicantId)) issue = "Applicant ID is required.";
    else if (blank(applicantName)) issue = "Applicant name is required.";
    else if (requestedLoanAmount == null || requestedLoanAmount.signum() <= 0) issue = "Requested loan amount must be positive.";
    else if (monthlyIncome == null || monthlyIncome.signum() <= 0) issue = "Monthly income must be positive.";
    else if (!oneOf(employmentStatus, "SALARIED", "SELF_EMPLOYED")) issue = "Employment status must be SALARIED or SELF_EMPLOYED.";
    else if (!oneOf(creditHistory, "GOOD", "AVERAGE", "POOR")) issue = "Credit history must be GOOD, AVERAGE, or POOR.";
    return map("validationResult", issue == null ? "VALID" : "INVALID",
        "validationMessage", issue == null ? "Applicant information passed validation." : issue);
  }

  @JobWorker(type = "validate-order", autoComplete = true)
  public Map<String, Object> validateOrder(
      @Variable String customerRef,
      @Variable String productId,
      @Variable Integer quantity,
      @Variable BigDecimal unitPrice,
      @Variable String customerCategory,
      @Variable String deliveryPreference,
      @Variable String paymentToken,
      @Variable Boolean simulateWorkerFailure) {
    failOnRequest(simulateWorkerFailure, "validate-order");
    String issue = null;
    if (blank(customerRef)) issue = "Customer reference is required.";
    else if (blank(productId)) issue = "Product ID is required.";
    else if (quantity == null || quantity < 1) issue = "Quantity must be at least one.";
    else if (unitPrice == null || unitPrice.signum() <= 0) issue = "Unit price must be positive.";
    else if (!oneOf(customerCategory, "STANDARD", "PREMIUM")) issue = "Customer category must be STANDARD or PREMIUM.";
    else if (!oneOf(deliveryPreference, "STANDARD", "EXPRESS")) issue = "Delivery preference must be STANDARD or EXPRESS.";
    else if (blank(paymentToken)) issue = "A mock payment token is required.";
    BigDecimal total = (quantity == null || unitPrice == null)
        ? BigDecimal.ZERO : unitPrice.multiply(BigDecimal.valueOf(quantity));
    return map("orderValid", issue == null, "orderValidationMessage", issue == null ? "Order fields are valid." : issue,
        "orderTotal", total, "currency", "INR");
  }

  @JobWorker(type = "check-inventory", autoComplete = true)
  public Map<String, Object> checkInventory(
      @Variable Integer quantity,
      @Variable Integer availableStock,
      @Variable Boolean simulateInventoryFailure) {
    failOnRequest(simulateInventoryFailure, "check-inventory");
    boolean available = quantity != null && availableStock != null && quantity > 0 && availableStock >= quantity;
    return map("stockAvailable", available,
        "inventoryStatus", available ? "AVAILABLE" : "INSUFFICIENT_STOCK");
  }

  @JobWorker(type = "validate-registration", autoComplete = true)
  public Map<String, Object> validateRegistration(
      @Variable String patientRef,
      @Variable String appointmentPreference,
      @Variable String symptomsSummary,
      @Variable String urgencyIndicator,
      @Variable Boolean simulateWorkerFailure) {
    failOnRequest(simulateWorkerFailure, "validate-registration");
    String issue = null;
    if (blank(patientRef)) issue = "Synthetic patient reference is required.";
    else if (blank(appointmentPreference)) issue = "Appointment preference is required.";
    else if (blank(symptomsSummary)) issue = "Synthetic symptoms summary is required.";
    else if (!oneOf(urgencyIndicator, "LOW", "MEDIUM", "HIGH")) issue = "Urgency indicator must be LOW, MEDIUM, or HIGH.";
    return map("registrationValid", issue == null,
        "registrationMessage", issue == null ? "Registration fields passed validation." : issue);
  }

  /**
   * The Lab 3 assignment specifically asks the Spring Boot worker to request availability.
   * The BPMN REST Connector then performs the orchestration-level availability call whose
   * result drives the routing gateway. Both requests are synthetic and idempotent.
   */
  @JobWorker(type = "check-appointment-availability", autoComplete = true)
  public Map<String, Object> checkAppointmentAvailability(
      @Variable String patientRef,
      @Variable String appointmentPreference,
      @Variable Boolean forceNoSlots,
      @Variable Boolean simulateSchedulingFailure) {
    try {
      Map<String, Object> requestBody = map(
          "patientRef", patientRef,
          "appointmentPreference", appointmentPreference,
          "forceNoSlots", Boolean.TRUE.equals(forceNoSlots),
          "simulateFailure", Boolean.TRUE.equals(simulateSchedulingFailure));
      HttpRequest request = HttpRequest.newBuilder()
          .uri(URI.create(mockApiBaseUrl + "/api/appointments/check"))
          .timeout(Duration.ofSeconds(15))
          .header("Content-Type", "application/json")
          .POST(HttpRequest.BodyPublishers.ofString(JSON.writeValueAsString(requestBody)))
          .build();
      HttpResponse<String> response = HTTP.send(request, HttpResponse.BodyHandlers.ofString());
      if (response.statusCode() < 200 || response.statusCode() >= 300) {
        throw new IllegalStateException("Scheduling availability pre-check returned HTTP "
            + response.statusCode() + ": " + response.body());
      }
      Map<String, Object> payload = JSON.readValue(response.body(), new TypeReference<Map<String, Object>>() {});
      Object slots = payload.get("slots");
      return map("workerAvailabilityChecked", true,
          "workerAppointmentAvailable", Boolean.TRUE.equals(payload.get("available")),
          "workerAvailableSlots", slots == null ? java.util.List.of() : slots,
          "workerSchedulingCheckMessage", "Availability pre-check completed by the Java Spring Boot worker.");
    } catch (InterruptedException ex) {
      Thread.currentThread().interrupt();
      throw new IllegalStateException("Scheduling availability pre-check was interrupted.", ex);
    } catch (Exception ex) {
      if (ex instanceof IllegalStateException) throw (IllegalStateException) ex;
      throw new IllegalStateException("Scheduling availability pre-check failed: " + ex.getMessage(), ex);
    }
  }

  private static void failOnRequest(Boolean requested, String worker) {
    if (Boolean.TRUE.equals(requested)) {
      throw new IllegalStateException("Intentional PBJ-2 recovery test failure in " + worker + ". Set the matching simulate flag to false, then retry the failed job in Operate.");
    }
  }

  private static boolean blank(String value) { return value == null || value.isBlank(); }
  private static boolean oneOf(String value, String... options) {
    if (value == null) return false;
    for (String option : options) if (option.equalsIgnoreCase(value)) return true;
    return false;
  }
  private static Map<String, Object> map(Object... pairs) {
    Map<String, Object> result = new LinkedHashMap<>();
    for (int i = 0; i < pairs.length; i += 2) result.put((String) pairs[i], pairs[i + 1]);
    return result;
  }
}
