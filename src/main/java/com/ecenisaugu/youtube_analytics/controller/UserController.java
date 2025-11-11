package com.ecenisaugu.youtube_analytics.controller;

import com.ecenisaugu.youtube_analytics.model.User;
import com.ecenisaugu.youtube_analytics.repository.UserRepository;
import com.ecenisaugu.youtube_analytics.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserRepository userRepository;
    private final UserService userService;


    public UserController(UserRepository userRepository, UserService userService) {
        this.userRepository = userRepository;
        this.userService = userService;
    }

    @GetMapping
    public List<User> getAllUsers(){
        return userRepository.findAll();
    }

    @PostMapping("/signUp")
    public ResponseEntity<?> saveUser(@RequestBody User user){
        User savedUser = userService.registerUser(user);


        /* SERVİS KULLANILMADAN KULLANICI KAYDI
        Optional<User> existingUser = userRepository.findByEmail(user.getEmail());
        if(existingUser.isPresent()){
            // kullanıcı zaten varsa 409 Conflict dön
            return ResponseEntity
                    .status(HttpStatus.CONFLICT)
                    .body("Bu e-posta adresiyle zaten bir kullanıcı mevcut.");
        }
        User savedUser = userRepository.save(user);
        System.out.println(user.toString());*/

        return ResponseEntity.ok(savedUser);
    }

    @PostMapping("/signIn")
    public ResponseEntity<?> signIn(@RequestBody User user){
        try {
            User loggedInUser = userService.loginUser(user.getEmail(), user.getPassword());
            return ResponseEntity.ok(loggedInUser);
        }catch (RuntimeException e){
            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .body(e.getMessage());
        }

    }

}
