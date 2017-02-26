import { NgModule } from '@angular/core';

import { OverlayComponent } from './overlay.component';
import { FullscreenDirective } from './fullscreen.directive';
import { AnimatedPathDirective } from './animated-path.directive';

@NgModule({
    imports: [],
    exports: [
        OverlayComponent,
        FullscreenDirective,
        AnimatedPathDirective
    ],
    declarations: [
        OverlayComponent,
        FullscreenDirective,
        AnimatedPathDirective
    ]
})
export class SharedModule {}