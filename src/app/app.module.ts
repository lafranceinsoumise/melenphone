import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { APP_BASE_HREF, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';
import { MaterialModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';
import { environment } from '../environments/environment';

import { AppRoutingModule } from './app-routing.module';
import { SharedModule } from './shared';

import { AppComponent } from './app.component';

import {
  AboutComponent,
  NavbarComponent,
  DynamicComponentComponent,
  GaugeComponent,
  CallMapComponent,
  AnimatedCallComponent,
  ToolbarUserInfoComponent,
  AchievementsComponent
} from './components';

import {
  FullscreenService,
  CoordinatesConverterService,
  SocketConnectionService,
  AuthenticationService,
  UserService,
  CallhubService,
  LeaderboardService,
  MapService
} from './shared';

import {
  ClassementComponent,
  HomeComponent,
  MesTropheesComponent,
  OauthRedirectComponent,
  PokechonHomeComponent,
  ProfileComponent
} from './views';
import { TrophiesComponent } from './components/trophies/trophies.component';



export function xsrfStrategyFactory() {
  return new CookieXSRFStrategy('csrftoken', 'X-CSRFToken');
}

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    DynamicComponentComponent,
    PokechonHomeComponent,
    GaugeComponent,
    ProfileComponent,
    CallMapComponent,
    AnimatedCallComponent,
    ToolbarUserInfoComponent,
    AchievementsComponent,
    MesTropheesComponent,
    AboutComponent,
    OauthRedirectComponent,
    ClassementComponent,
    TrophiesComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    HttpModule,
    MaterialModule.forRoot(),
    FlexLayoutModule.forRoot(),
    AppRoutingModule,
    SharedModule
  ],
  providers: [
    FullscreenService,
    {
      provide: APP_BASE_HREF,
      useValue: '/ng'
    },
    CoordinatesConverterService,
    SocketConnectionService,
    AuthenticationService,
    UserService,
    CallhubService,
    {
      provide: XSRFStrategy,
      useFactory: xsrfStrategyFactory
    },
    LeaderboardService,
    MapService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
