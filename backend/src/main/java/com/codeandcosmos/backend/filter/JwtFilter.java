package com.codeandcosmos.backend.filter;

import com.codeandcosmos.backend.enums.Role;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.service.AuthService;
import com.codeandcosmos.backend.util.JwtUtil;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@Component
@RequiredArgsConstructor
public class JwtFilter extends OncePerRequestFilter {
    private final JwtUtil jwtUtil;
    private final AuthService authService;

    private final List<String> unsecuredEndpoints = Arrays.asList(
            "/api/v1/authentication/login",
            "/api/v1/authentication/register");

    private final List<String> adminRoleBasedEndpoints = Arrays.asList(
            "/api/v1/admin/allPredictions",
            "/api/v1/admin/allProfile"
    );

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "*");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

        String path = request.getRequestURI();

        if (unsecuredEndpoints.contains(path)) {
            filterChain.doFilter(request, response);
            return;
        }

        String authorization = request.getHeader("Authorization");

        if (authorization == null || !authorization.startsWith("Bearer ")) {
            filterChain.doFilter(request,response);
            return;
        }

        String token = null;
        String email = null;

        try {
            token = authorization.substring(7);
            if (jwtUtil.isTokenExpired(token)) throw new JwtException("Token is expired");

            email = jwtUtil.extractEmail(token);
            User user = authService.getUser(email);

            if (adminRoleBasedEndpoints.contains(path) && !(user.getRole() == Role.ADMIN)) {
                throw new IllegalArgumentException("User is not permitted to user administrator services");
            }

            request.setAttribute("AuthenticatedUser", user);
            filterChain.doFilter(request,response);
        }catch (JwtException e) {
            filterChain.doFilter(request,response);
            return;
        }
    }
}
