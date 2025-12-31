package com.codeandcosmos.backend.dto.response;

import com.codeandcosmos.backend.model.Probabilities;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class PredictionResponse {
    private String PredictionResponse;
    private float confidence;
    private Probabilities probabilities;
}
