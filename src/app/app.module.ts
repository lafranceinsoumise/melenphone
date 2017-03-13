import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { APP_BASE_HREF, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';
import { MaterialModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AppRoutingModule } from './app-routing.module';
import { SharedModule } from './shared';

import { AppComponent } from './app.component';

import {
  HomeComponent,
  ConnectionComponent,
  PokechonHomeComponent,
  RegisterComponent,
  ClassementComponent
} from './views';

import {
  NavbarComponent,
  SidenavComponent,
  DynamicComponentComponent,
  GaugeComponent,
  RegistrationComponent,
  LoginComponent,
  CallMapComponent,
  AnimatedCallComponent,
  ToolbarUserInfoComponent
} from './components';

import {
  FullscreenService,
  CoordinatesConverterService,
  SocketConnectionService,
  AuthenticationService,
  UserService,
  CallhubService,
  LeaderboardService
} from './shared';
import { AchievementsComponent } from './components/achievements/achievements.component';
import { MesTropheesComponent } from './views/mes-trophees/mes-trophees.component';
import { AboutComponent } from './components/about/about.component';
import { OauthRedirectComponent } from './views/oauth-redirect/oauth-redirect.component';


export function xsrfStrategyFactory() {
  return new CookieXSRFStrategy('csrftoken', 'X-CSRFToken');
}

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidenavComponent,
    HomeComponent,
    LoginComponent,
    DynamicComponentComponent,
    PokechonHomeComponent,
    GaugeComponent,
    RegisterComponent,
    ConnectionComponent,
    CallMapComponent,
    AnimatedCallComponent,
    RegistrationComponent,
    ToolbarUserInfoComponent,
    AchievementsComponent,
    MesTropheesComponent,
    AboutComponent,
    OauthRedirectComponent,
    ClassementComponent
  ],
  imports: [
    BrowserAnimationsModule,
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
    LeaderboardService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
