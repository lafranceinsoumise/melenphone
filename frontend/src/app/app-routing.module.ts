import { NgModule } from '@angular/core';
import { Routes, RouterModule, ExtraOptions, PreloadAllModules } from '@angular/router';

import {
  HomeComponent,
  AproposComponent,
  PokechonHomeComponent,
  ProfileComponent,
  MesTropheesComponent,
  AvertissementComponent,
  OauthRedirectComponent,
  ClassementComponent,
  TemoignagesComponent,
  TutorielComponent,
} from './views';

import { AuthGuarg } from './_guards';

const routes: Routes = [
  {
    path: '',
    children: [
      { path: '', component: HomeComponent },
      { path: 'pokechon', loadChildren: './pokechon/pokechon.module#PokechonModule' },
      { path: 'profile', component: ProfileComponent },
      { path: 'classement', component: ClassementComponent },
      { path: 'mes-trophees', component: MesTropheesComponent },
      { path: 'connexion', component: AvertissementComponent },
      { path: 'oauth_redirect', component: OauthRedirectComponent },
      { path: 'apropos', component: AproposComponent },
      { path: 'temoignages', component: TemoignagesComponent },
      { path: 'tutoriel', component: TutorielComponent },
    ]
  }
];

const routerOptions: ExtraOptions = {
  enableTracing: false,
  preloadingStrategy: PreloadAllModules
};

@NgModule({
  imports: [RouterModule.forRoot(routes, routerOptions)],
  exports: [RouterModule],
  providers: []
})
export class AppRoutingModule { }
