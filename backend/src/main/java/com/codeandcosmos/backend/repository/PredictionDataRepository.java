package com.codeandcosmos.backend.repository;

import com.codeandcosmos.backend.model.PredictionData;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface PredictionDataRepository extends MongoRepository<PredictionData, String> {
    PredictionData findByUserId(String userId);
}
