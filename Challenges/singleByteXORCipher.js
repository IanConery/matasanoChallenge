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

var XORHash = {
  '00' : '0',
  '10' : '1',
  '01' : '1',
  '11' : '0'
};

var byteValues = [128,64,32,16,8,4,2,1];

var alphabet = {a:0,b:0,c:0,d:0,e:0,f:0,g:0,h:0,i:0,j:0,k:0,l:0,m:0,n:0,o:0,p:0,q:0,r:0,s:0,t:0,u:0,v:0,w:0,x:0,y:0,z:0};

var topOne = function(array){
  var mostCommon = [0, -1];
  array.forEach(function(string, index){
    var temp = 0;
    for(var i = 0; i < string.length; i++){
      alphabet[string[i]] ? temp += 1 : temp = temp;
    }
    if(temp > mostCommon[0]){
      mostCommon[0] = temp;
      mostCommon[1] = index; 
    }
    return array[mostCommon[1]]
  });
}

var hexToBinary = function(string){
  var result = '';
  for(var i = 0; i < string.length; i++){
    result += hexHash[string[i]];
  }
  return result;
}

var binToASCIICode = function(string){
  string = string.split('');
  var ASCIIValues = [];
  while(string.length >= 8){
    var temp = string.splice(0,8).join('');
    ASCIIValues.push(parseInt(temp, 2));
  }
  return ASCIIValues;
}

var ASCIIToChar = function(array){
  var result = '';
  array.forEach(function(code){
    result += String.fromCharCode(code);
  });
  return result;
}

var reverseXOR = function(encryptedByte, possKeyByte){
  var possOriginalByte = '';
  for(var i = 0; i < 8; i++){
    var tempBit = encryptedByte[i] + possKeyByte[i];
    possOriginalByte += XORHash[tempBit];
  }
  return possOriginalByte;
};

var decToBinary = function(base10){
  var binaryStr = '';
  for(var i = 0; i < byteValues.length; i++){
    if(base10 >= byteValues[i]){
      base10 = base10 - byteValues[i];
      binaryStr += '1';
    }else{
      binaryStr += '0';
    }
  }
  return binaryStr;
};

var charToHex = function(char){
  var bin = decToBinary(char.charCodeAt(0)).split('');
  var result = '';
  while(bin.length >= 4){
    var temp = bin.splice(0,4).join('');
    for(var key in hexHash){
      if(hexHash[key] === temp){
        result += key;
      }
    }
  }
  return result;
};


var singleByteCipher = function(string){
  string = hexToBinary(string).split('');
  var resultsArray = [];

  for(var i = 0; i < 128; i++){
    var test = decToBinary(i);
    var tempString = string.slice(0);
    var tempArray = [];

    while(tempString.length >= 8){
      var binChar = reverseXOR(tempString.splice(0,8).join('').toString(), test);
      binChar = binToASCIICode(binChar);
      tempArray.push(ASCIIToChar(binChar));
    }
    resultsArray.push(tempArray.join(''));
  }
  return resultsArray;
};

var stringToHex = function(string){
  var hexString = '';
  for(var i = 0; i < string.length; i++){
    hexString += charToHex(string[i]);
  }
  return hexString;
}

console.log(singleByteCipher('4554414f494e534852444c55'));
// console.log(stringToHex('ETAOINSHRDLU'))
//4554414f494e20534852444c55
//4554414f494e534852444c55
