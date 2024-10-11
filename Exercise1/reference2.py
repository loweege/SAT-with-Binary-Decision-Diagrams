class PermissiveConfigurationFinder:
    def __init__(self, clauses, features):
        # Clauses are in CNF form (list of lists with literals, where negative numbers represent negation)
        self.clauses = clauses
        self.features = features  # List of feature variables
        self.assignment = {}  # Stores partial configuration p: E → {0, 1}
    
    def is_valid_configuration(self, assignment):
        # Check if the current assignment satisfies all clauses
        for clause in self.clauses:
            satisfied = False
            for literal in clause:
                var = abs(literal)  # Get the variable ignoring negation
                value = self.assignment.get(var, None)
                
                # Handle positive and negative literals
                if literal > 0 and value is True:
                    satisfied = True
                elif literal < 0 and value is False:
                    satisfied = True
            
            if not satisfied:
                return False  # This clause is unsatisfied
        return True
    
    def find_permissive_configuration(self):
        for feature in self.features:
            # Try setting feature to True
            self.assignment[feature] = True
            if self.is_valid_configuration(self.assignment):
                # Check if this is permissive
                if self.is_permissive(feature):
                    continue
            # If setting to True does not work, try False
            self.assignment[feature] = False
            if not self.is_valid_configuration(self.assignment):
                raise ValueError(f"No permissive configuration found for feature {feature}")
    
    def is_permissive(self, feature):
        # Temporarily negate the feature's value
        original_value = self.assignment[feature]
        self.assignment[feature] = not original_value
        
        # Check if negating leads to invalid configurations for remaining features
        valid_with_negation = self.is_valid_configuration(self.assignment)
        
        # Restore the original value
        self.assignment[feature] = original_value
        
        return not valid_with_negation

# Example usage with negated variables
clauses = [[1, 2, 4], [-2, -4]]  # CNF form with negations
features = [0, 1, 2, 3, 4]
finder = PermissiveConfigurationFinder(clauses, features)
finder.find_permissive_configuration()
print(finder.assignment)
