package com.codeandcosmos.backend.service;

import com.codeandcosmos.backend.dto.request.ProfileRequest;
import com.codeandcosmos.backend.dto.response.ProfileResponse;
import com.codeandcosmos.backend.model.Profile;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.repository.ProfileRepository;
import com.codeandcosmos.backend.repository.UserRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestAttribute;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProfileService {
    private final ProfileRepository profileRepository;
    private final UserRepository userRepository;

    public void createProfile(User user, ProfileRequest profileRequest) {
        if (user.isProfileCreated()) throw new DuplicateKeyException("Profile already created");
        Profile profile = Profile.builder()
                .userId(user.getId())
                .firstName(profileRequest.getFirstName())
                .lastName(profileRequest.getLastName())
                .college(profileRequest.getCollege())
                .department(profileRequest.getDepartment())
                .semester(profileRequest.getSemester())
                .build();

        user.setProfileCreated(true);
        userRepository.save(user);

        profileRepository.save(profile);
    }

    public void updateProfile(User user, ProfileRequest profileRequest) {
        Profile profile = profileRepository.getProfileByUserId(user.getId());
        if (profile == null) throw new IllegalArgumentException("Profile not found");

        profile.setFirstName(profileRequest.getFirstName());
        profile.setLastName(profileRequest.getLastName());
        profile.setCollege(profileRequest.getCollege());
        profile.setDepartment(profileRequest.getDepartment());
        profile.setSemester(profileRequest.getSemester());

        profileRepository.save(profile);
    }

    public ProfileResponse getProfile(String userId) {
        Profile profile = profileRepository.getProfileByUserId(userId);

        return ProfileResponse.builder()
                .id(profile.getId())
                .userId(profile.getUserId())
                .firstName(profile.getFirstName())
                .lastName(profile.getLastName())
                .college(profile.getCollege())
                .department(profile.getDepartment())
                .semester(profile.getSemester())
                .createdDate(profile.getCreatedDate())
                .updatedAt(profile.getUpdatedAt())
                .build();
    }
}
