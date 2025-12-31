package com.codeandcosmos.backend.model;


import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Probabilities {
    @JsonProperty("At Risk")
    private Float atRisk;

    @JsonProperty("Average")
    private Float average;

    @JsonProperty("Good")
    private Float good;
}
