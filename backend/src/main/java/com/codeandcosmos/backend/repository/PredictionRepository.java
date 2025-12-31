package com.codeandcosmos.backend.repository;

import com.codeandcosmos.backend.model.Prediction;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface PredictionRepository extends MongoRepository<Prediction,String> {
    Prediction findPredictionByUserId(String userId);
}
