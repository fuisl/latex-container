# Use XeLaTeX as the default engine
$pdf_mode = 5;  # 5 = XeLaTeX

# Biber configuration
$biber = 'biber %O %S';
$bibtex_use = 2;  # Use biber instead of bibtex

# Maximum passes to prevent infinite loops (balanced for speed and stability)
$max_repeat = 5;

# Silent mode for faster builds (set to 0 to see all output for debugging)
$silent = 1;

# Enable glossaries support - simplified version
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

sub run_makeglossaries {
    my ($base) = @_;
    # Extract directory and basename
    my ($name, $path) = fileparse($base);
    # Change to output directory and run makeglossaries quietly
    my $ret = system("cd '$path' && makeglossaries -q '$name'");
    return $ret;
}

# Optimize: Only generate PDF, skip XDV intermediate
$xelatex = 'xelatex %O %S';

# Ensure latexmk knows about glossary files
$clean_ext .= ' %R.ist %R.acn %R.acr %R.alg %R.glg %R.glo %R.gls';

# Enable recorder to track file dependencies accurately
$recorder = 1;
