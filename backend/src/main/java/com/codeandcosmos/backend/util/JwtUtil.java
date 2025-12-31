package com.codeandcosmos.backend.util;

import com.codeandcosmos.backend.repository.ProfileRepository;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Component
@RequiredArgsConstructor
public class JwtUtil {
    @Value("${jwt.secret}")
    private String jwtSecret;

    private final ProfileRepository profileRepository;

    private SecretKey getKey(){
        return  Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
    }

    public String generateToken(String email){
        Map<String, Object> claims = new HashMap<>();
        return createToken(email, claims);
    }

    private String createToken(String email, Map<String, Object> claims){
        return Jwts.builder().
                subject(email).
                signWith(getKey()).
                claims(claims).
                issuedAt(new Date()).
                expiration(new Date(System.currentTimeMillis() + 7*3600*1000)).
                compact();
    }

    private Claims extractClaim(String token){
        return Jwts.parser()
                .verifyWith(getKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    public String extractEmail(String token){
        return extractClaim(token).getSubject();
    }

    public boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private Date extractExpiration(String token) {
        return extractClaim(token).getExpiration();
    }
}
