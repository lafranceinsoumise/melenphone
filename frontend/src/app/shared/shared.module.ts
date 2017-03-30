import { NgModule } from '@angular/core';

import { OverlayComponent } from './overlay.component';
import { FullscreenDirective } from './fullscreen.directive';
import { AnimatedPathComponent } from './animated-path.component';

@NgModule({
    imports: [],
    exports: [
        OverlayComponent,
        FullscreenDirective,
        AnimatedPathComponent
    ],
    declarations: [
        OverlayComponent,
        FullscreenDirective,
        AnimatedPathComponent
    ]
})
export class SharedModule {}