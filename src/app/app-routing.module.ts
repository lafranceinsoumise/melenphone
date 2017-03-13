import { NgModule } from '@angular/core';
import { Routes, RouterModule, ExtraOptions, PreloadAllModules } from '@angular/router';

import {
  HomeComponent,
  PokechonHomeComponent,
  ConnectionComponent,
  RegisterComponent,
  MesTropheesComponent
} from './views';

import { AuthGuarg } from './_guards';

const routes: Routes = [
  {
    path: '',
    children: [
      { path: '', component: HomeComponent },
      { path: 'pokechon', loadChildren: './pokechon/pokechon.module#PokechonModule' },
      { path: 'login', component: ConnectionComponent },
      { path: 'register', component: RegisterComponent },
      { path: 'mes-trophees', component: MesTropheesComponent }
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
