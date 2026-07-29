<?php

use Illuminate\Support\Facades\Artisan;

Artisan::command('about-engagement', function () {
    $this->info("Plateforme de l'engagement — backend des six premières pages.");
})->purpose('Display project information');
