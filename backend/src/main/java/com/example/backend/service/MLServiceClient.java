package com.example.backend.service;

import com.example.backend.dto.ExtractionResponseDto;
import com.example.backend.dto.ScoreRequestDto;
import com.example.backend.dto.ScoreResponseDto;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@Service
public class MLServiceClient {

    @org.springframework.beans.factory.annotation.Value("${ml.service.url:http://localhost:8000}")
    private String PYTHON_SERVICE_URL;
    private final RestTemplate restTemplate = new RestTemplate();

    public ExtractionResponseDto extractTextFromPdf(MultipartFile file) throws Exception {
        // 1. Prepare to send a file over the internet (Multipart Request)
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();

        // We have to turn the file into a Byte Array so Java can send it
        body.add("file", new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename(); // Keep the original name!
            }
        });

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        // 2. Make the POST request to our Python app
        String url = PYTHON_SERVICE_URL + "/extract-text";
        return restTemplate.postForObject(url, requestEntity, ExtractionResponseDto.class);
    }

    public ScoreResponseDto calculateScore(String resumeText, String jobDescriptionText) {
        // 1. Create our JSON package (Using our handy DTO Blueprint!)
        ScoreRequestDto requestDto = new ScoreRequestDto();
        requestDto.setResume_text(resumeText);
        requestDto.setJob_text(jobDescriptionText);

        // 2. Make the POST request
        String url = PYTHON_SERVICE_URL + "/score-match";
        return restTemplate.postForObject(url, requestDto, ScoreResponseDto.class);
    }
}
