package com.ecenisaugu.youtube_analytics.config;

import org.springframework.amqp.core.*;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {
    // application.properties' den değerleri alıyoruz
    @Value("${app.rabbit.exchange}")
    private String exchange;

    @Value("${app.rabbit.queue.link}")
    private String linkQueue;

    @Value("${app.rabbit.routing.link}")
    private String linkRoutingKey;

    // Queue oluştur
    @Bean
    public Queue commentQueue() {
        return QueueBuilder.durable(linkQueue).build();
    }

    @Bean
    public TopicExchange youtubeExchange() {
        return new TopicExchange(exchange);
    }

    // exchange ile queue bağlama
    @Bean
    public Binding commentBinding(){
        return BindingBuilder
                .bind(commentQueue())
                .to(youtubeExchange())
                .with(linkRoutingKey);
    }

    @Bean
    public Jackson2JsonMessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    public AmqpTemplate ampTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(messageConverter());
        return rabbitTemplate;
    }

}
