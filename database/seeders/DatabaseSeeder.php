<?php

namespace Database\Seeders;

use App\Enums\AccountStatus;
use App\Enums\EngagementType;
use App\Enums\OfferStatus;
use App\Enums\RemoteMode;
use App\Enums\UserRole;
use App\Enums\VerificationStatus;
use App\Models\Cause;
use App\Models\Country;
use App\Models\Language;
use App\Models\Offer;
use App\Models\Organization;
use App\Models\Skill;
use App\Models\SponsorSlot;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        foreach ([
            ['FR', 'France', 1],
            ['BE', 'Belgique', 2],
            ['CH', 'Suisse', 3],
            ['DZ', 'Algérie', 4],
            ['MA', 'Maroc', 5],
            ['TN', 'Tunisie', 6],
        ] as [$code, $name, $order]) {
            Country::updateOrCreate(['code' => $code], [
                'name_fr' => $name,
                'is_covered' => true,
                'sort_order' => $order,
            ]);
        }

        $causes = collect([
            'Éducation',
            'Inclusion numérique',
            'Environnement',
            'Santé',
            'Lutte contre la pauvreté',
            'Jeunesse',
            'Handicap',
            'Droits humains',
            'Aide humanitaire',
            'Gouvernance associative',
        ])->mapWithKeys(function (string $name, int $index) {
            $cause = Cause::updateOrCreate(['slug' => Str::slug($name)], [
                'name' => $name,
                'is_active' => true,
                'sort_order' => $index + 1,
            ]);

            return [$cause->slug => $cause];
        });

        $languages = collect([
            ['fr', 'Français'],
            ['ar', 'Arabe'],
            ['en', 'Anglais'],
            ['es', 'Espagnol'],
            ['de', 'Allemand'],
        ])->mapWithKeys(function (array $data) {
            $language = Language::updateOrCreate(['code' => $data[0]], [
                'name_fr' => $data[1],
                'is_active' => true,
            ]);

            return [$language->code => $language];
        });

        $skills = collect([
            'Gestion de projet',
            'Pédagogie',
            'Développement web',
            'Transformation numérique',
            'Comptabilité',
            'Collecte de fonds',
            'Communication',
            'Gouvernance',
            'Suivi et évaluation',
            'Formation',
        ])->mapWithKeys(function (string $name) {
            $skill = Skill::updateOrCreate(['slug' => Str::slug($name)], [
                'name' => $name,
                'is_active' => true,
            ]);

            return [$skill->slug => $skill];
        });

        $candidate = User::updateOrCreate(['email' => 'candidat@example.test'], [
            'name' => 'Nadia Benali',
            'password' => Hash::make('Password123!'),
            'role' => UserRole::Candidate,
            'status' => AccountStatus::Active,
            'email_verified_at' => now(),
            'locale' => 'fr',
        ]);

        $orgAdmin = User::updateOrCreate(['email' => 'organisation@example.test'], [
            'name' => 'Karim Haddad',
            'password' => Hash::make('Password123!'),
            'role' => UserRole::OrganizationAdmin,
            'status' => AccountStatus::Active,
            'email_verified_at' => now(),
            'locale' => 'fr',
        ]);

        $organizationsData = [
            [
                'name' => "Association Lumière d'Oran",
                'type' => 'association',
                'country_code' => 'DZ',
                'city' => 'Oran',
                'registry_number' => 'DZ-ORN-2014-00872',
                'size' => 'medium',
                'description' => "L'association accompagne les enfants et les jeunes d'Oran par des programmes éducatifs, culturels et d'inclusion numérique.",
                'mission' => "Réduire les inégalités éducatives et renforcer l'autonomie des jeunes.",
                'verification_status' => VerificationStatus::Verified,
                'founded_year' => 2014,
                'volunteer_count' => 86,
                'causes' => ['education', 'jeunesse', 'inclusion-numerique'],
            ],
            [
                'name' => 'Fondation Horizon Solidaire',
                'type' => 'foundation',
                'country_code' => 'FR',
                'city' => 'Paris',
                'registry_number' => 'FR-FND-2008-1193',
                'size' => 'large',
                'description' => "Fondation d'intérêt général qui finance et accompagne des projets d'inclusion, d'éducation et de transition numérique.",
                'mission' => "Accélérer des solutions sociales mesurables et durables.",
                'verification_status' => VerificationStatus::CertifiedPlus,
                'founded_year' => 2008,
                'volunteer_count' => 240,
                'causes' => ['inclusion-numerique', 'education', 'lutte-contre-la-pauvrete'],
            ],
            [
                'name' => 'Waqf El Baraka',
                'type' => 'waqf',
                'country_code' => 'TN',
                'city' => 'Tunis',
                'registry_number' => 'TN-WQF-2017-443',
                'size' => 'small',
                'description' => "Waqf dédié à l'éducation, à l'aide sociale et au financement de projets communautaires transparents.",
                'mission' => "Mettre les ressources philanthropiques au service de communautés autonomes.",
                'verification_status' => VerificationStatus::Verified,
                'founded_year' => 2017,
                'volunteer_count' => 42,
                'causes' => ['education', 'lutte-contre-la-pauvrete', 'gouvernance-associative'],
            ],
            [
                'name' => 'ONG Racines & Avenir',
                'type' => 'ngo',
                'country_code' => 'MA',
                'city' => 'Casablanca',
                'registry_number' => 'MA-ONG-2012-987',
                'size' => 'medium',
                'description' => "ONG marocaine active dans l'insertion des jeunes, l'entrepreneuriat social et le développement territorial.",
                'mission' => "Créer des parcours d'insertion et des opportunités économiques inclusives.",
                'verification_status' => VerificationStatus::Verified,
                'founded_year' => 2012,
                'volunteer_count' => 110,
                'causes' => ['jeunesse', 'lutte-contre-la-pauvrete', 'education'],
            ],
            [
                'name' => 'Humanité Sans Frontières',
                'type' => 'ngo',
                'country_code' => 'BE',
                'city' => 'Bruxelles',
                'registry_number' => 'BE-ONG-2010-2231',
                'size' => 'large',
                'description' => "Organisation humanitaire intervenant sur l'accès à la santé, la protection et la réponse d'urgence.",
                'mission' => "Protéger les personnes vulnérables et renforcer les acteurs locaux.",
                'verification_status' => VerificationStatus::CertifiedPlus,
                'founded_year' => 2010,
                'volunteer_count' => 410,
                'causes' => ['aide-humanitaire', 'sante', 'droits-humains'],
            ],
        ];

        $organizations = collect($organizationsData)->mapWithKeys(function (array $data) use ($orgAdmin, $causes) {
            $causeSlugs = $data['causes'];
            unset($data['causes']);

            $organization = Organization::updateOrCreate(
                ['slug' => Str::slug($data['name'])],
                [
                    ...$data,
                    'owner_user_id' => $orgAdmin->id,
                    'verified_at' => now()->subMonths(3),
                    'is_active' => true,
                ]
            );

            $organization->causes()->sync(
                collect($causeSlugs)->map(fn (string $slug) => $causes[$slug]->id)
            );

            return [$organization->slug => $organization];
        });

        $offers = [
            [
                'organization' => 'association-lumiere-doran',
                'title' => 'Coordinateur éducation',
                'engagement_type' => EngagementType::Employment,
                'employment_contract' => 'cdd',
                'country_code' => 'DZ',
                'city' => 'Oran',
                'remote_mode' => RemoteMode::OnSite,
                'description' => "Vous coordonnerez un programme d'accompagnement scolaire destiné à 300 enfants.\n\nLe poste implique la planification des activités, la coordination des bénévoles et le suivi des indicateurs.",
                'responsibilities' => "Planifier le programme éducatif.\nEncadrer les équipes bénévoles.\nAssurer le reporting mensuel.\nDévelopper les partenariats locaux.",
                'desired_profile' => "Expérience en coordination de projet, aisance relationnelle, maîtrise du français et de l'arabe.",
                'conditions' => "CDD de 6 mois renouvelable. Poste basé à Oran.",
                'duration_label' => '6 mois',
                'duration_days' => 180,
                'experience_level' => 'confirmed',
                'featured' => true,
                'causes' => ['education', 'jeunesse'],
                'languages' => ['fr', 'ar'],
                'skills' => ['gestion-de-projet', 'pedagogie', 'suivi-et-evaluation'],
            ],
            [
                'organization' => 'fondation-horizon-solidaire',
                'title' => 'Formateur numérique (mécénat)',
                'engagement_type' => EngagementType::SkillsSponsorship,
                'country_code' => 'FR',
                'city' => 'Paris',
                'remote_mode' => RemoteMode::Hybrid,
                'description' => "Concevoir et animer un parcours de formation numérique pour les équipes de trois associations partenaires.",
                'responsibilities' => "Évaluer les besoins.\nCréer les supports.\nAnimer quatre ateliers.\nRemettre un bilan et des recommandations.",
                'desired_profile' => "Collaborateur disposant d'une expérience en formation et transformation numérique.",
                'conditions' => "Mission réalisable sur trois mois, avec une partie à distance.",
                'duration_label' => '10 jours-homme',
                'duration_days' => 10,
                'experience_level' => 'senior',
                'featured' => true,
                'causes' => ['inclusion-numerique'],
                'languages' => ['fr'],
                'skills' => ['formation', 'transformation-numerique'],
            ],
            [
                'organization' => 'waqf-el-baraka',
                'title' => 'Administrateur bénévole',
                'engagement_type' => EngagementType::Governance,
                'country_code' => 'TN',
                'city' => 'Tunis',
                'remote_mode' => RemoteMode::Hybrid,
                'description' => "Le Waqf recherche un administrateur indépendant pour renforcer sa gouvernance et son comité d'audit.",
                'responsibilities' => "Participer aux conseils trimestriels.\nContribuer au contrôle interne.\nAccompagner la stratégie de transparence.",
                'desired_profile' => "Expérience en finance, audit, droit ou gouvernance.",
                'conditions' => "Mandat bénévole de deux ans, renouvelable une fois.",
                'duration_label' => 'Mandat 2 ans',
                'duration_days' => 730,
                'experience_level' => 'governance',
                'featured' => true,
                'causes' => ['gouvernance-associative'],
                'languages' => ['fr', 'ar'],
                'skills' => ['gouvernance', 'comptabilite'],
            ],
            [
                'organization' => 'ong-racines-avenir',
                'title' => 'Chargé de projet (CDD)',
                'engagement_type' => EngagementType::Employment,
                'employment_contract' => 'cdd',
                'country_code' => 'MA',
                'city' => 'Casablanca',
                'remote_mode' => RemoteMode::Hybrid,
                'description' => "Pilotage opérationnel d'un programme d'insertion professionnelle pour des jeunes éloignés de l'emploi.",
                'responsibilities' => "Suivre les bénéficiaires.\nCoordonner les partenaires.\nProduire les rapports bailleurs.",
                'desired_profile' => "Deux ans d'expérience en gestion de projet social.",
                'conditions' => "CDD de 12 mois.",
                'duration_label' => '12 mois',
                'duration_days' => 365,
                'experience_level' => 'confirmed',
                'featured' => true,
                'causes' => ['jeunesse', 'lutte-contre-la-pauvrete'],
                'languages' => ['fr', 'ar'],
                'skills' => ['gestion-de-projet', 'suivi-et-evaluation'],
            ],
            [
                'organization' => 'humanite-sans-frontieres',
                'title' => 'Consultant suivi-évaluation',
                'engagement_type' => EngagementType::Consulting,
                'country_code' => 'BE',
                'city' => 'Bruxelles',
                'remote_mode' => RemoteMode::Remote,
                'description' => "Mission de consultance pour revoir le cadre de suivi-évaluation d'un programme humanitaire régional.",
                'duration_label' => '25 jours',
                'duration_days' => 25,
                'experience_level' => 'expert',
                'featured' => false,
                'causes' => ['aide-humanitaire'],
                'languages' => ['fr', 'en'],
                'skills' => ['suivi-et-evaluation'],
            ],
            [
                'organization' => 'association-lumiere-doran',
                'title' => 'Développeur Laravel bénévole',
                'engagement_type' => EngagementType::Volunteering,
                'country_code' => 'DZ',
                'city' => 'Oran',
                'remote_mode' => RemoteMode::Remote,
                'description' => "Améliorer l'outil interne de suivi des bénéficiaires et documenter son déploiement.",
                'duration_label' => '8 semaines',
                'duration_days' => 56,
                'experience_level' => 'confirmed',
                'featured' => false,
                'causes' => ['inclusion-numerique', 'education'],
                'languages' => ['fr'],
                'skills' => ['developpement-web'],
            ],
            [
                'organization' => 'ong-racines-avenir',
                'title' => 'Designer freelance pour campagne jeunesse',
                'engagement_type' => EngagementType::Freelance,
                'country_code' => 'MA',
                'city' => 'Casablanca',
                'remote_mode' => RemoteMode::Remote,
                'description' => "Créer l'identité visuelle et les supports numériques d'une campagne dédiée à l'emploi des jeunes.",
                'duration_label' => '4 semaines',
                'duration_days' => 28,
                'experience_level' => 'confirmed',
                'featured' => false,
                'causes' => ['jeunesse'],
                'languages' => ['fr'],
                'skills' => ['communication'],
            ],
        ];

        foreach ($offers as $position => $data) {
            $orgSlug = $data['organization'];
            $causeSlugs = $data['causes'];
            $languageCodes = $data['languages'];
            $skillSlugs = $data['skills'];
            unset($data['organization'], $data['causes'], $data['languages'], $data['skills']);

            $offer = Offer::updateOrCreate(
                ['slug' => Str::slug($data['title']).'-'.($position + 1)],
                [
                    ...$data,
                    'organization_id' => $organizations[$orgSlug]->id,
                    'uuid' => (string) Str::uuid(),
                    'status' => OfferStatus::Published,
                    'published_at' => now()->subDays($position + 1),
                    'expires_at' => now()->addMonths(3),
                    'contact_email' => $orgAdmin->email,
                ]
            );

            $offer->causes()->sync(collect($causeSlugs)->map(fn ($slug) => $causes[$slug]->id));
            $offer->languages()->sync(collect($languageCodes)->map(fn ($code) => $languages[$code]->id));
            $offer->skills()->sync(
                collect($skillSlugs)->mapWithKeys(fn ($slug) => [$skills[$slug]->id => ['is_required' => true]])
            );
        }

        SponsorSlot::updateOrCreate(['placement' => 'homepage'], [
            'sponsor_name' => 'Partenaire éthique',
            'label' => 'Partenariat',
            'copy' => 'Emplacement réservé à un annonceur aligné avec les valeurs de la plateforme.',
            'target_url' => null,
            'starts_at' => now()->subDay(),
            'ends_at' => now()->addYear(),
            'is_active' => true,
        ]);
    }
}
