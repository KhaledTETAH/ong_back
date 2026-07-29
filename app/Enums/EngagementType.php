<?php

namespace App\Enums;

enum EngagementType: string
{
    case Volunteering = 'volunteering';
    case Employment = 'employment';
    case Freelance = 'freelance';
    case Consulting = 'consulting';
    case Governance = 'governance';
    case SkillsSponsorship = 'skills_sponsorship';

    public function label(): string
    {
        return match ($this) {
            self::Volunteering => 'Bénévolat',
            self::Employment => 'Salariat',
            self::Freelance => 'Freelance',
            self::Consulting => 'Consultance',
            self::Governance => 'Mandat',
            self::SkillsSponsorship => 'Mécénat de compétences',
        };
    }
}
