var hexHash = {
  '0' : '0000',
  '1' : '0001',
  '2' : '0010',
  '3' : '0011',
  '4' : '0100',
  '5' : '0101',
  '6' : '0110',
  '7' : '0111',
  '8' : '1000',
  '9' : '1001',
  'a' : '1010',
  'b' : '1011',
  'c' : '1100',
  'd' : '1101',
  'e' : '1110',
  'f' : '1111'
};


var repeatingKeyXOR = function(string, key){
  var keyLength = key.length;
  var xoredBinaryString = '';
  var encryptedString = '';
  var counter = 0;
  for(var i = 0; i < string.length; i++){
    var binChar = string[i].charCodeAt(0).toString(2).split('');
    while(binChar.length < 8){
      binChar.unshift('0');
    }
    if(counter === key.length){
      counter = 0;
    }
    var binKeyChar = key[counter].charCodeAt(0).toString(2).split('');
    while(binKeyChar.length < 8){
      binKeyChar.unshift('0');
    }
    for(var j = 0; j < 8; j++){
      xoredBinaryString += binChar[j] ^ binKeyChar[j];
    }
    counter++;
  }
  xoredBinaryString = xoredBinaryString.split('');
  while(xoredBinaryString.length >= 4){
    var temp = xoredBinaryString.splice(0,4).join('');
    for(var key in hexHash){
      if(hexHash[key] === temp){
        encryptedString += key;
      }
    }
  }
  return encryptedString;
};

console.log(repeatingKeyXOR("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", 'ICE'));
console.log('0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f')