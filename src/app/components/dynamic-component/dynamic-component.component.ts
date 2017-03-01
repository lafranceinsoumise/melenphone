import { Component, OnInit, ViewContainerRef, ViewChild, ComponentFactoryResolver, Input, ReflectiveInjector } from '@angular/core';

@Component({
  selector: 'jlm-dynamic-component',
  entryComponents: [],
  template: `<div #dynamicComponentContainer></div>`,
  styleUrls: ['./dynamic-component.component.scss']
})
export class DynamicComponentComponent implements OnInit {
  currentComponent = null;
  @ViewChild('dynamicComponentContainer', { read: ViewContainerRef })
  dynamicComponentContainer: ViewContainerRef;

  @Input()
  set componentData(data: {component: any, inputs: any}) {
    if (!data) {
      return;
    }

    const inputProviders = Object.keys(data.inputs)
        .map(inputName => {
          return {
            provide: inputName,
            useValue: data.inputs[inputName]
          };
        });
    const resolvedInputs = ReflectiveInjector.resolve(inputProviders);
    const injector = ReflectiveInjector.fromResolvedProviders(
      resolvedInputs, 
      this.dynamicComponentContainer.parentInjector
    );
    const factory = this.resolver.resolveComponentFactory(data.component);
    const component = factory.create(injector);
    this.dynamicComponentContainer.insert(component.hostView);
    if (this.currentComponent) {
      this.currentComponent.destroy();
    }

  }

  constructor(private resolver: ComponentFactoryResolver) { }

  ngOnInit() {
  }

}
