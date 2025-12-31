package com.codeandcosmos.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Document(collection = "prediction data")
public class PredictionData {
    @Indexed(unique = true)
    private String userId;
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
