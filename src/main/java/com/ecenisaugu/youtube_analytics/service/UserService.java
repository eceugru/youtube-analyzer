package com.ecenisaugu.youtube_analytics.service;

import com.ecenisaugu.youtube_analytics.model.User;
import com.ecenisaugu.youtube_analytics.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public User registerUser(User user) {
        // Email kontrolü
        if (userRepository.findByEmail(user.getEmail()).isPresent()) {
            throw new RuntimeException("Bu e-posta ile kullanıcı zaten var");
        }
        // Şifrenin hashlenmesi
        String password = passwordEncoder.encode(user.getPassword());
        user.setPassword(password);

        // kaydet
        return userRepository.save(user);
    }

    public User loginUser(String email, String password) {
        User user = userRepository.findByEmail(email).orElseThrow(()-> new RuntimeException("Kullanıcı bulunamadı !"));

        boolean isPasswordMatch = passwordEncoder.matches(password, user.getPassword());
        if (!isPasswordMatch) {
            throw new  RuntimeException("Hatalı şifre !");
        }
        return user;
    }
}
