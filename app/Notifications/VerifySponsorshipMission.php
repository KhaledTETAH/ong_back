<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Notification;

class VerifySponsorshipMission extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(private readonly string $plainToken)
    {
    }

    public function via(object $notifiable): array
    {
        return ['mail'];
    }

    public function toMail(object $notifiable): MailMessage
    {
        $url = route('sponsorship.verify', [
            'trackingUuid' => $notifiable->tracking_uuid,
            'token' => $this->plainToken,
        ]);

        return (new MailMessage)
            ->subject('Confirmez votre dépôt de mission de mécénat')
            ->greeting('Bonjour,')
            ->line('Nous avons reçu votre proposition de mission de mécénat de compétences.')
            ->action('Confirmer mon adresse e-mail', $url)
            ->line('Après confirmation, la mission sera transmise à l’équipe de modération.')
            ->line('Si vous n’êtes pas à l’origine de cette demande, ignorez ce message.');
    }
}
