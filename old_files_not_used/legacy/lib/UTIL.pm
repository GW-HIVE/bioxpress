#!/usr/bin/perl

sub GetDeviceType{

    my $list = qq{iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm};
    my @devlist = split(/\|/, $list);

    if($ENV{HTTP_USER_AGENT} =~ m/mobile/i == 1){
       foreach my $dev (@devlist){
          if($ENV{HTTP_USER_AGENT} =~ m/$dev/i == 1){
             return $dev;
          }
       }
       return qq{unknownmobile};
    }
    else{
       return qq{pc};
    }
}



sub LoadParams{
    my($configfile) = @_;

    my @lines = `cat $configfile`;
    foreach my $line (@lines){
       my ($param, @a) = split(/\t+/, Trim($line));
       $param = uc(Trim($param)); 
       my $val = join("\t", @a);
       $PHASH{$param} .= Trim($val);
   }
}


sub LoadVariables{

    my @plist = $CGI_OBJ->param();
    foreach my $p (@plist){
       my $var = uc($p);
       $VHASH{$var} = $CGI_OBJ->param($p);
   }

}


sub WriteFile {
    my ($buffer, $fname) = @_; 
    unless (open(FW, ">$fname")){    
        print "\nCould not open file for writing: \"$fname\"\n\n";
        exit;
    }
    print FW "$buffer";
    close(FW);
}


sub GetTimeStamp{
    my ($sec, $min, $hour, $day, $month, $year) = (localtime)[0, 1, 2, 3, 4, 5];
    $month += 1;
    $year += 1900;
    
    return qq{$year-$month-$day-$hour-$min-$sec};

}


sub GetErr{
    my($msg) = @_;
    return qq{<font color=red>$msg</font>};
}


sub GetMsg{
    my($color, $msg) = @_;
    return qq{<font style="color:$color;">$msg</font>};
}



sub IsDir {  
    my ($dir) = @_;
    if(opendir(DIR, $dir)){
        close(DIR);
        return 1;
    }
    else{
        return 0;    
    }
}


sub IsFile {  
    my ($file) = @_;
    if(open(FR, $file)){
        close(FR);
        return 1;
    }
    else{
        return 0;    
    }
}


sub Trim {
    my $string = shift;
    for ($string) {
        s/^\s+//;
        s/\s+$//;
    }
    return $string;
}



1;
