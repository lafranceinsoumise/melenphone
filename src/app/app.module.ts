import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { APP_BASE_HREF } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { MaterialModule } from '@angular/material';
import { AppRoutingModule } from './app-routing.module';
import { SharedModule } from './shared/shared.module';

import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { SidenavComponent } from './components/sidenav/sidenav.component';
import { HomeComponent } from './views/home/home.component';
import { DynamicComponentComponent } from './components/dynamic-component/dynamic-component.component';
import { RiriComponent } from './components/widgets/riri/riri.component';
import { FifiComponent } from './components/widgets/fifi/fifi.component';
import { LoulouComponent } from './components/widgets/loulou/loulou.component';
import { PokechonHomeComponent } from './views/pokechon-home/pokechon-home.component';
import { GaugeComponent } from './components/gauge/gauge.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { ConnectionComponent } from './views/connection/connection.component';
import { CallMapComponent } from './components/call-map/call-map.component';

import { FullscreenService } from './shared/fullscreen.service';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidenavComponent,
    HomeComponent,
    LoginComponent,
    DynamicComponentComponent,
    RiriComponent,
    FifiComponent,
    LoulouComponent,
    PokechonHomeComponent,
    GaugeComponent,
    RegisterComponent,
    LoginComponent,
    ConnectionComponent,
    CallMapComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterialModule.forRoot(),
    AppRoutingModule,
    SharedModule
  ],
  providers: [
    FullscreenService,
    {provide: APP_BASE_HREF, useValue: '/ng'}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
