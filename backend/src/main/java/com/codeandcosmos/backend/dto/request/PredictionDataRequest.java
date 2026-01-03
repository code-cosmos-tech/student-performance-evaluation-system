package com.codeandcosmos.backend.dto.request;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class PredictionDataRequest {
      private float lastSemSPI;
      private float internalAssessmentAvg;
      private float attendancePercentage;
      private int totalBacklogs;
      private int pyqSolvingFrequency;
      private float studyHoursWeekly;
      private String sleepCategory;
      private float gamingHoursWeekly;
      private int assignmentDelayCount;
      private String department;
      private String travelTimeCategory;
      private String extraCurricularLevel;
}
