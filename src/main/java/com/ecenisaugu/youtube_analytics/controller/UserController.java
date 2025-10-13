package com.ecenisaugu.youtube_analytics.controller;

import com.ecenisaugu.youtube_analytics.model.User;
import com.ecenisaugu.youtube_analytics.repository.UserRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping
    public List<User> getAllUsers(){
        return userRepository.findAll();
    }

    @PostMapping("/login")
    public User saveUser(@RequestBody User user){
        System.out.println(user.toString());
        return userRepository.save(user);
    }
}
