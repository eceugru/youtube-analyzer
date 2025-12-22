package com.ecenisaugu.youtube_analytics.service;

import java.util.Map;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class VideoCompareProducer {
    private final RabbitTemplate rabbitTemplate;

    @Value("${app.rabbit.exchange}")
    private String exchange;

    @Value("${app.rabbit.routing.transcript}")
    private String routingKey;

    public VideoCompareProducer(RabbitTemplate rabbitTemplate){
        this.rabbitTemplate = rabbitTemplate;
    }

    public void sendVideoUrls(Map<String,String> payload){
        System.out.println("Video linkleri gönderiliyor: " + payload);
        rabbitTemplate.convertAndSend(exchange, routingKey, payload);
    }
    
}
