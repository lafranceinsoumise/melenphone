import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { APP_BASE_HREF, CommonModule } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpModule, XSRFStrategy, CookieXSRFStrategy } from '@angular/http';
import { MaterialModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { StoreModule } from '@ngrx/store';

import { environment } from '../environments/environment';

import { AppRoutingModule } from './app-routing.module';
import { SharedModule } from './shared';

import { AppComponent } from './app.component';

import {
  DynamicComponentComponent,
  GaugeComponent,
  CallMapComponent,
  AnimatedCallComponent,
  NavToolbarComponent,
  ToptenComponent,
  FooterComponent,
  AchievementComponent
} from './components';

import {
  FullscreenService,
  CoordinatesConverterService,
  SocketConnectionService,
  AuthenticationService,
  UserService,
  CallhubService,
  LeaderboardService,
  MapService,
  BasicService,
} from './shared';

import {
  AproposComponent,
  ClassementComponent,
  HomeComponent,
  AvertissementComponent,
  MesTropheesComponent,
  OauthRedirectComponent,
  PokechonHomeComponent,
  ProfileComponent,
  TutorielComponent
} from './views';

import { reducer } from './rx/reducers';

export function xsrfStrategyFactory() {
  return new CookieXSRFStrategy('csrftoken', 'X-CSRFToken');
}

@NgModule({
  declarations: [
    AppComponent,
    AproposComponent,
    HomeComponent,
    DynamicComponentComponent,
    PokechonHomeComponent,
    GaugeComponent,
    ProfileComponent,
    CallMapComponent,
    AnimatedCallComponent,
    NavToolbarComponent,
    AvertissementComponent,
    MesTropheesComponent,
    OauthRedirectComponent,
    ClassementComponent,
    ToptenComponent,
    AproposComponent,
    FooterComponent,
    AchievementComponent,
    TutorielComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    FormsModule,
    HttpModule,
    MaterialModule.forRoot(),
    FlexLayoutModule.forRoot(),
    StoreModule.provideStore(reducer),
    SimpleNotificationsModule.forRoot(),
    AppRoutingModule,
    SharedModule
  ],
  entryComponents: [ AchievementComponent ],
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
    MapService,
    BasicService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
