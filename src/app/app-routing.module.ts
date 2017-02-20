import { NgModule } from '@angular/core';
import { Routes, RouterModule, ExtraOptions, PreloadAllModules } from '@angular/router';

import { HomeComponent } from './views/home/home.component';
import { PokechonHomeComponent } from './views/pokechon-home/pokechon-home.component';

const routes: Routes = [
  {
    path: '',
    children: [
      { path: '', component: HomeComponent },
      { path: 'pokechon', loadChildren: './pokechon/pokechon.module#PokechonModule' }
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
