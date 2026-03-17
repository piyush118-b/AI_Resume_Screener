package com.example.backend.controller;

import com.example.backend.dto.ScoreResponseDto;
import com.example.backend.service.ResumeOrchestratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller; // We use @Controller for HTML Pages, not @RestController
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@Controller // This tells Spring "I am serving Web Pages using Thymeleaf!"
@RequestMapping("/dashboard")
public class DashboardController {

    @Autowired
    private ResumeOrchestratorService orchestratorService;

    // 🌟 When the user visits 'localhost:8080/dashboard' they see the beautiful
    // form!
    @GetMapping({ "", "/" })
    public String viewDashboard() {
        return "index"; // This points to resources/templates/index.html
    }

    // 🌟 When the user clicks the "Run AI Analysis" button on our web page
    @PostMapping("/analyze")
    public String analyzeFromWeb(
            @RequestParam("file") MultipartFile file,
            @RequestParam("job_description") String jobDescription,
            Model textInjector) { // "Model" is Thymeleaf's way of injecting data into the HTML

        try {
            // Run our python microservice ML pipeline
            ScoreResponseDto result = orchestratorService.processNewResume(file, jobDescription);

            // 🌟 We take the Math Box and shove it into the HTML using the label "score"
            textInjector.addAttribute("score", result);

            // Send the user to the result page (results.html)
            return "result";

        } catch (Exception e) {
            e.printStackTrace();
            textInjector.addAttribute("error", "The AI Engines crashed! Check the console.");
            return "index"; // Kick them back to the start
        }
    }
}
