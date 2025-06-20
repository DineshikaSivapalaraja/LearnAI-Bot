package com.pdfchat.backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;


@SpringBootApplication
@RestController
public class BackendApplication {

	public static void main(String[] args) {	
		SpringApplication.run(BackendApplication.class, args);
	}

	@GetMapping("/")
	public String hello() {
		return "Hello!";
	}


}
