package com.codeandcosmos.backend.controller;

import com.codeandcosmos.backend.dto.request.PredicationDataRequest;
import com.codeandcosmos.backend.model.Prediction;
import com.codeandcosmos.backend.model.PredictionData;
import com.codeandcosmos.backend.model.Profile;
import com.codeandcosmos.backend.model.User;
import com.codeandcosmos.backend.payload.Response;
import com.codeandcosmos.backend.repository.UserRepository;
import com.codeandcosmos.backend.service.AdminService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/admin")
@RequiredArgsConstructor
public class AdminController {
    private final AdminService adminService;
    private final UserRepository userRepository;

    @GetMapping("/allProfile")
    public ResponseEntity<List<Profile>> getAllProfile() {
        return ResponseEntity.ok(adminService.getAllProfiles());
    }

    @GetMapping("/allPredictions")
    public ResponseEntity<List<Prediction>> getAllPredictions() {
        return ResponseEntity.ok(adminService.getAllPredictions());
    }

    @PostMapping("/predictAll")
    public ResponseEntity<Response> predictAll() {
        adminService.predictAllStudentPerformance();

        Response response = Response.builder()
                .message("predicted all predictions")
                .build();
        return ResponseEntity.ok(response);
    }

    @PostMapping("/addData/{id}")
    public ResponseEntity<Response> addStudentData(@PathVariable("id") String id, @RequestBody PredicationDataRequest predicationDataRequest) {
        adminService.addData(id, predicationDataRequest);

        Response response = Response.builder()
                .message("added data successfully")
                .build();
        return ResponseEntity.ok(response);
    }

}
