package com.codeandcosmos.backend.service;

import com.codeandcosmos.backend.dto.request.UserRequest;
import com.codeandcosmos.backend.enums.Role;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.repository.UserRepository;
import com.codeandcosmos.backend.util.Encoder;
import com.codeandcosmos.backend.util.JwtUtil;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepository userRepository;
    private final Encoder encoder;
    private final JwtUtil jwtUtil;

    public User getUser(String email) {
        return userRepository.findByEmail(email).orElseThrow(()->new IllegalArgumentException("User not found"));
    }

    public void register(@Valid UserRequest userRequest) {
        User user = User.builder()
                .email(userRequest.getEmail())
                .password(encoder.encode(userRequest.getPassword()))
                .role(Role.USER)
                .build();
        userRepository.save(user);
    }

    public String login(@Valid UserRequest userRequest) {
        User user = getUser(userRequest.getEmail());
        if (!encoder.matchPassword(userRequest.getPassword(), user.getPassword())){
            throw new IllegalArgumentException("Wrong password");
        }
        return jwtUtil.generateToken(user.getEmail());
    }
}
