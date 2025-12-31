package com.codeandcosmos.backend.repository;

import com.codeandcosmos.backend.model.Profile;
import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.Optional;

public interface ProfileRepository extends MongoRepository<Profile,String> {
    Profile getProfileByUserId(String userId);

    Optional<Profile> findByUserId(String userId);
}
