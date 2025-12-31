package com.codeandcosmos.backend.service;

import com.codeandcosmos.backend.dto.request.PredicationDataRequest;
import com.codeandcosmos.backend.model.Prediction;
import com.codeandcosmos.backend.model.PredictionData;
import com.codeandcosmos.backend.model.Profile;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.repository.PredictionDataRepository;
import com.codeandcosmos.backend.repository.PredictionRepository;
import com.codeandcosmos.backend.repository.ProfileRepository;
import com.codeandcosmos.backend.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Service
@RequiredArgsConstructor
public class AdminService {
    private final ProfileRepository profileRepository;
    private final PredictionRepository predictionRepository;
    private final UserRepository userRepository;
    private final PredictionDataRepository predictionDataRepository;
    private final RestTemplate restTemplate;
    private final PredictionService predictionService;

    public List<Profile> getAllProfiles() {
        return profileRepository.findAll();
    }

    public List<Prediction> getAllPredictions() {
        return predictionRepository.findAll();
    }

    public void addData(String id, PredicationDataRequest predicationDataRequest) {
        User user = userRepository.findById(id).orElseThrow(()->new IllegalArgumentException("user not found"));
        Profile profile = profileRepository.findByUserId(id).orElseThrow(()->new IllegalArgumentException("profile not found"));

        PredictionData predictionData = preparePredictionData(id, profile.getDepartment(), predicationDataRequest);

        predictionDataRepository.save(predictionData);
    }

    private PredictionData preparePredictionData(String userId, String departmentName, PredicationDataRequest predicationDataRequest) {
        return PredictionData.builder()
                .userId(userId)
                .lastSemSPI(predicationDataRequest.getLastSemSPI())
                .internalAssessmentAvg(predicationDataRequest.getInternalAssessmentAvg())
                .assignmentDelayCount(predicationDataRequest.getAssignmentDelayCount())
                .attendancePercentage(predicationDataRequest.getAttendancePercentage())
                .department(departmentName)
                .totalBacklogs(predicationDataRequest.getTotalBacklogs())
                .extraCurricularLevel(predicationDataRequest.getExtraCurricularLevel())
                .gamingHoursWeekly(predicationDataRequest.getGamingHoursWeekly())
                .pyqSolvingFrequency(predicationDataRequest.getPyqSolvingFrequency())
                .sleepCategory(predicationDataRequest.getSleepCategory())
                .studyHoursWeekly(predicationDataRequest.getStudyHoursWeekly())
                .travelTimeCategory(predicationDataRequest.getTravelTimeCategory())
                .build();
    }

    public void predictAllStudentPerformance() {
        List<PredictionData> predictionDataList = predictionDataRepository.findAll();

        ExecutorService executorService = Executors.newFixedThreadPool(10);

        predictionDataList.forEach(data->{
            PredicationDataRequest predicationDataRequest = convertToPredicationDataRequest(data);
            predictionService.predict(data.getUserId(), predicationDataRequest);
        });
    }

    public PredicationDataRequest convertToPredicationDataRequest(PredictionData data) {
        return PredicationDataRequest.builder()
                .lastSemSPI(data.getLastSemSPI())
                .internalAssessmentAvg(data.getInternalAssessmentAvg())
                .assignmentDelayCount(data.getAssignmentDelayCount())
                .attendancePercentage(data.getAttendancePercentage())
                .department(data.getDepartment())
                .totalBacklogs(data.getTotalBacklogs())
                .extraCurricularLevel(data.getExtraCurricularLevel())
                .gamingHoursWeekly(data.getGamingHoursWeekly())
                .pyqSolvingFrequency(data.getPyqSolvingFrequency())
                .sleepCategory(data.getSleepCategory())
                .studyHoursWeekly(data.getStudyHoursWeekly())
                .travelTimeCategory(data.getTravelTimeCategory())
                .build();
    }
}
