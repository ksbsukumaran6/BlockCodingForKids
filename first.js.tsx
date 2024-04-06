console.log("Hello Suku")
import React from 'react';

interface MyComponentProps {
  name: string;
  age: number;
}

class MyComponent extends React.Component<Readonly<MyComponentProps>> {
  render() {
    return (
      <div>
        <p>Name: {this.props.name}</p>
        <p>Age: {this.props.age}</p>
      </div>
    );
  }
}

export default MyComponent;