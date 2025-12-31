package com.codeandcosmos.backend.controller;

import com.codeandcosmos.backend.dto.request.UserRequest;
import com.codeandcosmos.backend.dto.response.TokenResponse;
import com.codeandcosmos.backend.payload.Response;
import com.codeandcosmos.backend.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/v1/authentication")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<Response> register(@Valid @RequestBody UserRequest user) {
        authService.register(user);

        Response response = Response.builder()
                .message("User registered successfully!")
                .build();
        return ResponseEntity.ok(response);
    }

    @PostMapping("/login")
    public ResponseEntity<TokenResponse> login(@Valid @RequestBody UserRequest user) {
        String token = authService.login(user);
        TokenResponse tokenResponse = TokenResponse.builder()
                .token(token)
                .timestamp(LocalDateTime.now())
                .build();
        return ResponseEntity.ok(tokenResponse);
    }
}
