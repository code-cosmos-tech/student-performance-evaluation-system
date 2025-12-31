package com.codeandcosmos.backend.globalExceptionHandler;

import com.codeandcosmos.backend.payload.Response;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ExceptionHandlers {
    @ExceptionHandler(DuplicateKeyException.class)
    public ResponseEntity<Response> duplicateKeyExceptionHandler(DuplicateKeyException e) {
        Response response = Response.builder()
                .message(e.getMessage())
                .build();

        return ResponseEntity.badRequest().body(response);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Response> illegalArgumentExceptionHandler(IllegalArgumentException e) {
        Response response = Response.builder()
                .message(e.getMessage())
                .build();

        return ResponseEntity.badRequest().body(response);
    }
}
