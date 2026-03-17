package com.example.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration // Marks this as a Config File so Spring Boot runs it when it starts over
@EnableWebSecurity // Turns on all the cool lock-and-key powers!
public class SecurityConfig {

    /**
     * Think of this like a bouncer at a club. Right now, to keep testing easy,
     * we are telling the bouncer to let everyone inside!
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http
                .csrf(csrf -> csrf.disable()) // Turning off a browser-based security lock for API testing
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/v1/resume/scan").permitAll() // Letting our scan endpoint be public
                        .requestMatchers("/dashboard/**", "/css/**").permitAll() // Let anyone view the website graphics
                        .anyRequest().authenticated());

        return http.build();
    }
}
