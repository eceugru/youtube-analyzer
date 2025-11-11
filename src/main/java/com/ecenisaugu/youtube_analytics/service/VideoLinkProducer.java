package com.ecenisaugu.youtube_analytics.service;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class VideoLinkProducer {
    private final RabbitTemplate rabbitTemplate;

    @Value("${app.rabbit.exchange}")
    private String exchange;

    @Value("${app.rabbit.routing.link}")
    private String routingKey;

    public VideoLinkProducer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void sendVideoUrl(String videoUrl) {
        System.out.println(" Video link RabbitMQ'ya gönderiliyor: " + videoUrl);
        rabbitTemplate.convertAndSend(exchange, routingKey, videoUrl);
    }
}
