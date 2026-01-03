package com.codeandcosmos.backend.controller;

import com.codeandcosmos.backend.dto.request.PredictionDataRequest;
import com.codeandcosmos.backend.dto.response.PredictionResponse;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.service.PredictionService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/predict")
@RequiredArgsConstructor
public class PredictionController {
    private final PredictionService predictionService;

    @PostMapping
    public ResponseEntity<PredictionResponse> getPrediction(@RequestAttribute("AuthenticatedUser") User user, @Valid @RequestBody PredictionDataRequest predicationDataRequest){
        return ResponseEntity.ok().body(predictionService.predict(user.getId(), predicationDataRequest));
    }

}
