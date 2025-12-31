package com.codeandcosmos.backend.model;

import com.codeandcosmos.backend.dto.response.PredictionResponse;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Document(collection = "predictions")
public class Prediction {
    @Id
    private String id;
    @Indexed
    private String userId;
    @NotBlank
    private PredictionResponse prediction;
}
