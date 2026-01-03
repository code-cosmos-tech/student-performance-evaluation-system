package com.codeandcosmos.backend.service;

import com.codeandcosmos.backend.dto.request.PredictionDataRequest;
import com.codeandcosmos.backend.dto.response.PredictionResponse;
import com.codeandcosmos.backend.model.Prediction;
import com.codeandcosmos.backend.model.PredictionData;
import com.codeandcosmos.backend.repository.PredictionRepository;
import com.codeandcosmos.backend.repository.ProfileRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class PredictionService {
    private final RestTemplate restTemplate;
    private final ProfileRepository profileRepository;
    private final PredictionRepository predictionRepository;

    public PredictionResponse predict(String userId, PredictionDataRequest predicationDataRequest) {

        PredictionResponse predictionResponse = restTemplate.postForEntity(
                "https://student-performance-ml-service.onrender.com/api/v1/ml/predict",
                predicationDataRequest,
                PredictionResponse.class
        ).getBody();

        Prediction prediction = predictionRepository.findPredictionByUserId(userId);
        if (prediction == null) {
            prediction = Prediction.builder()
                    .userId(userId)
                    .build();
        }
        prediction.setPrediction(predictionResponse);

        predictionRepository.save(prediction);

        return predictionResponse;
    }
}
