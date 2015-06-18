#include <Servo.h> 
 
Servo servox; 
Servo servoy;

int i =0;
String command;
void setup()
{
  Serial.begin(115200);
  servox.attach(9);
  servoy.attach(10);
}

void loop()
{
}

void serialEvent() {
  char character = (char)Serial.read();
  
  if(character == 'Z')
  {
    switch (command.charAt(0))
    {
      case 'X':
      servox.write(command.substring(1, 4).toInt());
      break; 
      case 'Y':
      servoy.write(command.substring(1, 4).toInt());
      break;
    }
    i=0;
    command=""; 
  } 
  else
  {
    if (i<4)
    {
      command +=character;
      i++;
    }
    else
    {
      i=0;
      command="";
    }
  }
}
