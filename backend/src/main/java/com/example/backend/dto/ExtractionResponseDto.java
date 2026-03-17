package com.example.backend.dto;

import lombok.Data;
import java.util.Map;

@Data
public class ExtractionResponseDto {
    private String filename;
    private String status;
    private Map<String, Object> extracted_data;
    private Integer raw_text_length;
    private String text;
}
