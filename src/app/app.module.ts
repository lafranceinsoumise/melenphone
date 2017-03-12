import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { APP_BASE_HREF } from '@angular/common';
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
  RegisterComponent
} from './views';

import {
  NavbarComponent,
  SidenavComponent,
  DynamicComponentComponent,
  GaugeComponent,
  RegistrationComponent,
  LoginComponent,
  CallMapComponent,
  AnimatedCallComponent
} from './components';

import {
  FullscreenService,
  CoordinatesConverterService,
  SocketConnectionService,
  AuthenticationService,
  UserService } from './shared';
import { ToolbarUserInfoComponent } from './components/toolbar-user-info/toolbar-user-info.component';

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
    ToolbarUserInfoComponent
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
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
    {
      provide: XSRFStrategy,
      useFactory: xsrfStrategyFactory
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
