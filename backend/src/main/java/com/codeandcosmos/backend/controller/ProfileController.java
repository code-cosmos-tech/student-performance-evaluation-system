package com.codeandcosmos.backend.controller;

import com.codeandcosmos.backend.dto.request.ProfileRequest;
import com.codeandcosmos.backend.dto.response.ProfileResponse;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.payload.Response;
import com.codeandcosmos.backend.service.ProfileService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/profile")
@RequiredArgsConstructor
public class ProfileController {
    private final ProfileService profileService;

    @PostMapping("/create")
    public ResponseEntity<Response> createProfile(@RequestAttribute("AuthenticatedUser") User user, @Valid @RequestBody ProfileRequest profileRequest) {
        profileService.createProfile(user, profileRequest);

        Response response = Response.builder()
                .message("Profile created successfully")
                .build();
        return ResponseEntity.ok(response);
    }

    @PutMapping("/update")
    public ResponseEntity<Response> updateProfile(@RequestAttribute("AuthenticatedUser") User user, @RequestBody @Valid ProfileRequest profileRequest) {
        profileService.updateProfile(user, profileRequest);

        Response response = Response.builder()
                .message("Profile updated successfully")
                .build();
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<ProfileResponse> getProfile(@RequestAttribute("AuthenticatedUser") User user) {
        return ResponseEntity.ok(profileService.getProfile(user.getId()));
    }
}
