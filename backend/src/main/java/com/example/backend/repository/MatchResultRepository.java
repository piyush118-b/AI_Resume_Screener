package com.example.backend.repository;

import com.example.backend.entity.MatchResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MatchResultRepository extends JpaRepository<MatchResult, Long> {
}
